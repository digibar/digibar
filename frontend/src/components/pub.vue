<template>
  <div class="pub">
    <div id="container" class="container_thjs">
    </div>
    <div id="calls">
    </div>
  </div>
</template>

<script>
import * as THREE from 'three'

import Stats from 'three/examples/jsm/libs/stats.module.js';

import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { LightProbeGenerator } from 'three/examples/jsm/lights/LightProbeGenerator.js';

//mapping from scene objects to tabe ids
var sceneTableIds = {"SM_Table_1B": "a",
                      "SM_Table_2B": "2",
                      "SM_Counter": "3"}

export default {
  name: 'Pub',
    data() {
      return {
        stream: undefined,
        callElements: {}
      };
    },
    components: {

    },
    computed: {
      bar() {
        var request = new XMLHttpRequest();
        request.open('GET', this.$appConfig.backend_uri + 'bars', false);
        request.send();
        window.console.log("test");
        var matching = undefined;
        if (request.status === 200) {
            var res = JSON.parse(request.responseText);

          //window.console.log(item.result);
          matching = res.find((barName) => {
            return barName.id === this.$route.params.id;
          });
        }
        return matching ? matching : []
      },

      callParams() {
        var abw = this.$appConfig.audio_bandwith;
        var vbw = this.$appConfig.video_bandwith;
        return {
          'sdpTransform': function(sdp) {
            // https://stackoverflow.com/questions/16712224/how-to-control-bandwidth-in-webrtc-video-call/16868123#16868123
            sdp = sdp.replace(/a=mid:audio\r\n/g, 'a=mid:audio\r\nb=AS:' + abw + '\r\n');
            sdp = sdp.replace(/a=mid:video\r\n/g, 'a=mid:video\r\nb=AS:' + vbw + '\r\n');
            return sdp;
          }
        }
      }
    },
    methods: {
      doJoin() {
        //evt.preventDefault();
        var barId = this.$route.params.id;
        var tables = this.getTables(barId);
        if (tables !== undefined) {
          console.log(tables);
          tables[0].guests.forEach(userId => {
            this.call(userId);
          });
        }
      },

      joinTable(bar_id, table_id) {
          console.log("joining table: " + table_id);

          var data = JSON.stringify({'user': this.$peer.id});
          var request = new XMLHttpRequest();
          request.open('POST', this.$appConfig.backend_uri + 'bars/' + bar_id + '/tables/' + table_id + '/join', false);
          request.send(data);
      },

      leaveTable(bar_id, table_id){
          console.log("leaving table: " + table_id);

          var data = JSON.stringify({'user': this.$peer.id});
          var request = new XMLHttpRequest();
          request.open('POST', this.$appConfig.backend_uri + 'bars/' + bar_id + '/tables/' + table_id + '/leave', false);
          request.send(data);
      },

      getTables(bar_id) {
        var request = new XMLHttpRequest();
        request.open('GET', this.$appConfig.backend_uri + 'bars/' + bar_id + '/tables', false);
        request.send();
        if (request.status === 200) {
            var res = JSON.parse(request.responseText);

            //window.console.log(item.result);
            return res;
        }
        return [];
      },

      call(userId) {
        console.log('Calling ' + userId);
        var call = this.$peer.call(userId, this.stream, this.callParams);
        var vid = document.createElement("video");
        var cont = document.getElementById('calls');
        vid.setAttribute('id', userId);
        this.callElements[userId] = call;
        cont.appendChild(vid);
        call.on('stream', function(remoteStream) {
            vid.srcObject = remoteStream;
            vid.play();
        });
      },

      buildScene: function(){
          var camera, scene, renderer, dirLight, hemiLight, visitor;
          var mixers = [];
          var stats;
          var app = this;
          var bar = this.$route.params.id;

          var clock = new THREE.Clock();
          var mouse = new THREE.Vector2();
          var raycaster = new THREE.Raycaster();

          var chairs = {};

          var backendURI = this.$appConfig.backend_uri;

          var controls = undefined;

          init();
          animate();

          function init() {

              var container = document.getElementById( 'container' );

              camera = new THREE.PerspectiveCamera( 30, container.offsetWidth / container.offsetHeight, 1, 5000 );
              camera.position.set( 0, 750, -750 );

              scene = new THREE.Scene();
              scene.background = new THREE.Color().setHSL(0, 0, 0);
              //scene.fog = new THREE.Fog( scene.background, 1, 7500 );

              // LIGHTS

              hemiLight = new THREE.HemisphereLight( 0xffffff, 0xffffff, 0.46 );
              hemiLight.color.setHSL( 0.6, 1, 0.6 );
              hemiLight.groundColor.setHSL( 0.095, 1, 0.75 );
              hemiLight.position.set( 0, 50, 0 );
              //scene.add( hemiLight );

              //

              dirLight = new THREE.DirectionalLight( 0xffffff, 1 );
              dirLight.color.setHSL( 0.1, 1, 0.95 );
              dirLight.position.set( - 1, 1.75, 1 );
              dirLight.position.multiplyScalar( 35 );
              //scene.add( dirLight );

              dirLight.castShadow = true;

              dirLight.shadow.mapSize.width = 512;
              dirLight.shadow.mapSize.height = 512;

              var d = 250;

              dirLight.shadow.camera.left = - d;
              dirLight.shadow.camera.right = d;
              dirLight.shadow.camera.top = d;
              dirLight.shadow.camera.bottom = - d;

              dirLight.shadow.camera.far = 3500;
              dirLight.shadow.bias = - 0.0005;

              //light probe
              var lightProbe = new THREE.LightProbe();
              scene.add( lightProbe );

              console.log("loading cubemaps");

              var urls = genCubeUrls( '/bar/cubemap/', '.png' );

              new THREE.CubeTextureLoader().load( urls, function ( cubeTexture ) {

                  cubeTexture.encoding = THREE.sRGBEncoding;

                  lightProbe.copy( LightProbeGenerator.fromCubeTexture( cubeTexture ) );
              });

              // MODEL

              var loader = new GLTFLoader();

              console.log("loading scene");

              loader.load( '/bar/visitor.glb', function ( gltf ) {

                  visitor = gltf.scene.children[ 0 ];

              });

              loader.load( '/bar/bar.glb', function ( gltf ) {

                  console.log("scene loaded");

                  var objects = gltf.scene;

                  console.log(dumpObject(objects).join('\n'));

                  objects.traverse( function ( child ) {

                      if ( child.isMesh) {

                          child.material.side = THREE.FrontSide;
                      }

                  } );

                  scene.add(objects);

              } );

              // RENDERER

              renderer = new THREE.WebGLRenderer( { antialias: true } );
              renderer.setPixelRatio( window.devicePixelRatio );
              renderer.setSize( container.offsetWidth, container.offsetHeight );
              container.appendChild( renderer.domElement );
              renderer.outputEncoding = THREE.sRGBEncoding;
              renderer.shadowMap.enabled = false;

              //controls
              controls = new OrbitControls( camera, renderer.domElement );
              controls.update()

              container.addEventListener( 'click', onMouseClick, false );

              // STATS

              stats = new Stats();
              container.appendChild( stats.dom );
          }

          //

          function animate() {

              requestAnimationFrame( animate );

              render();
              stats.update();

          }

          function render() {

              var delta = clock.getDelta();

              for ( var i = 0; i < mixers.length; i ++ ) {

                  mixers[ i ].update( delta );

              }

              renderer.render( scene, camera );

              //camera.position = camera.position;

          }

          function onMouseClick(event){
              raycast(event);
          }

          function raycast ( e ) {
              //set the mouse position with a coordinate system where the center
              //of the screen is the origin
              var container = document.getElementById( 'container' );
              var rect = container.getBoundingClientRect();
              mouse.x = ( (e.clientX - rect.left) / container.offsetWidth ) * 2 - 1;
              mouse.y = - ( (e.clientY - rect.top) / container.offsetHeight ) * 2 + 1;

              //set the picking ray from the camera position and mouse coordinates
              raycaster.setFromCamera( mouse, camera );

              //compute intersections
              var intersects = raycaster.intersectObjects( scene.children, true);

              updateTables();

              for ( var i = 0; i < intersects.length; i++ ) {
                  //if(intersects[i].object.name != ""){
                  //    console.log( intersects[ i ] );
                  //}
                  /*
                      An intersection has the following properties :
                          - object : intersected object (THREE.Mesh)
                          - distance : distance from camera to intersection (number)
                          - face : intersected face (THREE.Face3)
                          - faceIndex : intersected face index (number)
                          - point : intersection point (THREE.Vector3)
                          - uv : intersection point in the object's UV coordinates (THREE.Vector2)
                  */

                  if(intersects[i].object.name.includes("Table")){

                      var obj = intersects[i].object;

                      var tables = getTables(bar);

                      var table_id = getKeyByValue(tables, "id", sceneTableIds[intersects[i].object.name])

                      console.log(tables[table_id]);

                      if(!(tables[table_id].guests.includes(app.$peer.id))){
                          //spawnVisitor(obj);
                          console.log("attempting join");
                          app.doJoin();
                          joinTable(obj, bar, sceneTableIds[obj.name]);
                          updateTables();
                          break;

                      }else{
                          //var obj_r = scene.getObjectByName(chairs[obj.name]["mesh"]);
                          //console.log( "deleting " + obj_r);
                          //scene.remove(obj_r);
                          leaveTable(bar, sceneTableIds[obj.name]);
                          updateTables();
                          for (let [id, stream] of Object.entries(app.callElements)) {
                            stream.close();
                            var elem = document.getElementById(id);
                            if (elem !== undefined) {
                              document.getElementById('calls').removeChild(elem);
                            }
                            console.log(id);
                          }
                          app.callElements = {}
                      }
                  }
              }

          }

          function updateTables(){
              removeAllVisitors();
              var tables = getTables(bar);
              console.log(tables);
              for (var table_name in sceneTableIds) {
                  console.log(scene.getObjectByName(table_name));
                  var table_id = sceneTableIds[table_name]
                  console.log("updating table: " + table_name + " with id: " + table_id);
                  if(getKeyByValue(tables, "id", table_id) != undefined){
                      updateTable(scene.getObjectByName(table_name), tables[getKeyByValue(tables, "id", table_id)].guests);
                  }
              }
          }

          function updateTable(tableObj, users){
              for (var i = 0; i < users.length; i++) {
                  if(!(tableObj.name in chairs) && i < tableObj.children.length){
                      console.log("adding visitor");
                      console.log(tableObj.children[i]);
                      spawnVisitor(tableObj.children[i], users[i]);
                  }
              }
          }

          function removeAllVisitors(){
              chairs = [];
              console.log(scene);
              scene.children.forEach( function ( child ) {
                  if ( child.name.includes("pants_")) {

                      scene.remove(child);
                  }

              } );

              console.log(dumpObject(scene).join('\n'));
          }

          function spawnVisitor(targetObj, username){
              console.log(username);

              chairs[targetObj.name] = {};

              var tpos = new THREE.Vector3(targetObj.position.x, targetObj.position.y, targetObj.position.z);
              tpos.setFromMatrixPosition( targetObj.matrixWorld );
              var trot = new THREE.Euler();
              var position = new THREE.Vector3();
              var quaternion = new THREE.Quaternion();
              var scale = new THREE.Vector3();

              targetObj.matrixWorld.decompose( position, quaternion, scale );

              trot.setFromQuaternion(quaternion);

              var mesh = visitor.clone();
              var userFrame = document.getElementById(username);

              if(userFrame !== undefined){
                  var videoTexture = new THREE.VideoTexture( userFrame );
                  var videoMaterial = new THREE.MeshBasicMaterial( { map: videoTexture } );

                  mesh.children.forEach( function ( child ) {
                      if ( child.name.includes("Plane")) {
                          child.material = videoMaterial;
                      }

                  } );
              }

              mesh.name += targetObj.name;

              console.log(targetObj.parent.name);
              console.log("table id: " + sceneTableIds[targetObj.parent.name]);

              console.log(tpos);
              mesh.position.set(tpos.x, tpos.y, tpos.z);
              mesh.rotation.set(trot.x, trot.y, trot.z);
              scene.add(mesh);
          }

          function dumpObject(obj, lines = [], isLast = true, prefix = '') {
            const localPrefix = isLast ? '└─' : '├─';
            lines.push(`${prefix}${prefix ? localPrefix : ''}${obj.name || '*no-name*'} [${obj.type}]`);
            const newPrefix = prefix + (isLast ? '  ' : '│ ');
            const lastNdx = obj.children.length - 1;
            obj.children.forEach((child, ndx) => {
              const isLast = ndx === lastNdx;
              dumpObject(child, lines, isLast, newPrefix);
            });
            return lines;
          }

          function genCubeUrls( prefix, postfix ) {

              return [
                  prefix + 'px' + postfix, prefix + 'nx' + postfix,
                  prefix + 'py' + postfix, prefix + 'ny' + postfix,
                  prefix + 'pz' + postfix, prefix + 'nz' + postfix
              ];

          }

          function getTables(bar_id){
              var request = new XMLHttpRequest();
              request.open('GET', backendURI + '/bars/' + bar_id + '/tables', false);
              request.send();
              window.console.log("test");
              if (request.status === 200) {
                  var res = JSON.parse(request.responseText);

                  window.console.log(res);
                  return res;
              }
              return [{guests: [], id: "1"}]
          }

          function joinTable(targetObj, bar_id, table_id){
            console.log("joining table: " + table_id);

            //controls.target = new THREE.Vector3(targetObj.parent.position.x, targetObj.parent.position.y + 50, targetObj.parent.position.z);
            //controls.maxDistance = 350;
            //controls.enablePan = false;
            //controls.update();

            app.joinTable(bar_id, table_id);
          }

          function leaveTable(bar_id, table_id){
            //controls.target = new THREE.Vector3(0, 0, 0);
            //controls.maxDistance = 1500;
            //controls.enablePan = true;
            //controls.reset();
            //controls.update();

            app.leaveTable(bar_id, table_id);
          }

          function getKeyByValue(object, property, value) {
            return Object.keys(object).find(key => object[key][property] === value);
          }
      }
    },
    mounted: function() {
      var getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
      var app = this;
      getUserMedia({video: { width: {max: 640}, height: {max: 480} }, audio: true}, function(stream) {
          app.stream = stream;
          var vid = document.createElement("video");
          var cont = document.getElementById('calls');
          cont.appendChild(vid);
          vid.setAttribute('id', app.$peer.id);
          vid.srcObject = stream;
          vid.play();
      }, function(err) {
          console.log('Failed to get local stream' ,err);
      });
      this.$peer.on('call', function(call) {
          call.answer(app.stream, app.callParams); // Answer the call with an A/V stream.
          var vid = document.createElement("video");
          var cont = document.getElementById('calls');
          vid.setAttribute('id', call.peer);
          cont.appendChild(vid);
          app.callElements[call.peer] = call;
          call.on('stream', function(remoteStream) {
              // gets called twice: https://github.com/peers/peerjs/issues/609
              vid.srcObject = remoteStream;
              vid.play();
          });
      });
      this.buildScene();
    }
}
</script>

<style>
    .container_thjs {
        width: 80%;
        height: 80vh;
    }
</style>