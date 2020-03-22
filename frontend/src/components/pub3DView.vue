<template>
    <div>
        <div id="container"></div>
        <div id="info">
            <a href="https://threejs.org" target="_blank" rel="noopener">three.js</a> - webgl hemisphere light example<br/>
            <button id="hemisphereButton">toggle hemisphere light</button>
            <button id="directionalButton">toggle directional light</button>
            <video id="blubb" autoplay style="display:none"></video>
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
    var sceneTableIds = {"SM_Table_1B": "1",
                         "SM_Table_2B": "2",
                         "SM_Counter": "3"}

    var bar = "corona-bar"

    export default {
        name: "pub3DView",

        data() {
            return {};
        },

        mounted(){
            this.onReady();
        },

        methods: {
            onReady: function(){
                console.log("blb");
                var camera, scene, renderer, dirLight, dirLightHeper, hemiLight, hemiLightHelper, visitor;
                var mixers = [];
                var stats;

                var clock = new THREE.Clock();
                var mouse = new THREE.Vector2();
                var raycaster = new THREE.Raycaster();

                var chairs = {};

                var backendURI = this.$appConfig.backend_uri;

                var controls = undefined;
                //var videoMaterial = undefined;


                init();
                animate();

                function init() {

                    var container = document.getElementById( 'container' );

                    var video = document.getElementById( 'blubb' );

                    if ( navigator.mediaDevices && navigator.mediaDevices.getUserMedia ) {

                        var constraints = { video: { width: 1280, height: 720, facingMode: 'user' } };

                        navigator.mediaDevices.getUserMedia( constraints ).then( function ( stream ) {

                            // apply the stream to the video element used in the texture

                            video.srcObject = stream;
                            video.play();

                        } ).catch( function ( error ) {

                            console.error( 'Unable to access the camera/webcam.', error );

                        } );

                    } else {

                        console.error( 'MediaDevices interface not available.' );

                    }


                    camera = new THREE.PerspectiveCamera( 30, window.innerWidth / window.innerHeight, 1, 5000 );
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

                    hemiLightHelper = new THREE.HemisphereLightHelper( hemiLight, 10 );
                    //scene.add( hemiLightHelper );

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

                    dirLightHeper = new THREE.DirectionalLightHelper( dirLight, 10 );
                    //scene.add( dirLightHeper );

                    //light probe
                    var lightProbe = new THREE.LightProbe();
                    scene.add( lightProbe );

                    console.log("loading cubemaps");

                    var urls = genCubeUrls( 'bar/cubemap/', '.png' );

                    new THREE.CubeTextureLoader().load( urls, function ( cubeTexture ) {

                        cubeTexture.encoding = THREE.sRGBEncoding;

                        lightProbe.copy( LightProbeGenerator.fromCubeTexture( cubeTexture ) );
                    });

                    // MODEL

                    var loader = new GLTFLoader();

                    console.log("loading scene");

                    loader.load( 'bar/visitor.glb', function ( gltf ) {

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

                        //var mixer = new THREE.AnimationMixer( mesh );
                        //mixer.clipAction( gltf.animations[ 0 ] ).setDuration( 1 ).play();
                        //mixers.push( mixer );

                    } );

                    // RENDERER

                    renderer = new THREE.WebGLRenderer( { antialias: true } );
                    renderer.setPixelRatio( window.devicePixelRatio );
                    renderer.setSize( window.innerWidth, window.innerHeight );
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


                    window.addEventListener( 'resize', onWindowResize, false );

                    var hemisphereButton = document.getElementById( 'hemisphereButton' );
                    hemisphereButton.addEventListener( 'click', function () {

                        hemiLight.visible = ! hemiLight.visible;
                        hemiLightHelper.visible = ! hemiLightHelper.visible;

                    } );

                    var directionalButton = document.getElementById( 'directionalButton' );
                    directionalButton.addEventListener( 'click', function () {

                        dirLight.visible = ! dirLight.visible;
                        dirLightHeper.visible = ! dirLightHeper.visible;

                    } );

                }

                function onWindowResize() {

                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();

                    renderer.setSize( window.innerWidth, window.innerHeight );

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

                //function onMouseMove( event ) {
                //
                //  mouse.x = ( event.clientX - windowHalf.x );
                //  mouse.y = ( event.clientY - windowHalf.x );
                //
                //}

                //function onMouseWheel( event ) {
                //
                //  camera.position.z += event.deltaY * 0.1; // move camera along z-axis
                //
                //}

                function onMouseClick(event){
                    raycast(event);
                }

                function raycast ( e ) {
                    //set the mouse position with a coordinate system where the center
                    //of the screen is the origin
                    mouse.x = ( e.clientX / window.innerWidth ) * 2 - 1;
                    mouse.y = - ( e.clientY / window.innerHeight ) * 2 + 1;

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

                        if(intersects[i].object.name.includes("Stool")){

                            var obj = intersects[i].object;

                            if(!(obj.name in chairs)){
                                //spawnVisitor(obj);
                                joinTable(obj, bar, sceneTableIds[obj.parent.name]);
                                updateTables();
                                break;

                            }else{
                                //var obj_r = scene.getObjectByName(chairs[obj.name]["mesh"]);
                                //console.log( "deleting " + obj_r);
                                //scene.remove(obj_r);
                                leaveTable(bar, sceneTableIds[obj.parent.name]);
                                updateTables();
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
                        if(!(tableObj.name in chairs)){
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

                    var video = document.getElementById( username );

                    var videoTexture = new THREE.VideoTexture( video );
                    var videoMaterial = new THREE.MeshBasicMaterial( { map: videoTexture } );

                    mesh.children.forEach( function ( child ) {
                        if ( child.name.includes("Plane")) {
                            child.material = videoMaterial;
                        }

                    } );

                    mesh.name += targetObj.name;

                    //chairs[targetObj.name]["mesh"] = mesh.name;

                    console.log(targetObj.parent.name);
                    console.log("table id: " + sceneTableIds[targetObj.parent.name]);

                    console.log(tpos);
                    mesh.position.set(tpos.x, tpos.y, tpos.z);
                    mesh.rotation.set(trot.x, trot.y, trot.z);
                    scene.add(mesh);

                    /*loader.load( 'bar/visitor.glb', function ( gltf ) {

                        var mesh = gltf.scene.children[ 0 ];
                        mesh.name += targetObj.name;

                        chairs[targetObj.name]["mesh"] = mesh.name;

                        console.log(targetObj.parent.name);
                        console.log("table id: " + sceneTableIds[targetObj.parent.name]);

                        console.log(tpos);
                        mesh.position.set(tpos.x, tpos.y, tpos.z);
                        mesh.rotation.set(trot.x, trot.y, trot.z);
                        scene.add(mesh);

                    });*/
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

                    controls.target = new THREE.Vector3(targetObj.parent.position.x, targetObj.parent.position.y + 50, targetObj.parent.position.z);
                    controls.maxDistance = 350;
                    controls.enablePan = false;
                    controls.update();

                    var data = JSON.stringify({'user': 'blubb'});
                    var request = new XMLHttpRequest();
                    request.open('POST', backendURI + '/bars/' + bar_id + '/tables/' + table_id + '/join', false);
                    request.send(data);

                }

                function leaveTable(bar_id, table_id){
                    console.log("leaving table: " + table_id);
                    controls.target = new THREE.Vector3(0, 0, 0);
                    controls.maxDistance = 1500;
                    controls.enablePan = true;
                    controls.reset();
                    controls.update();

                    var data = JSON.stringify({'user': 'blubb'});
                    var request = new XMLHttpRequest();
                    request.open('POST', backendURI + '/bars/' + bar_id + '/tables/' + table_id + '/leave', false);
                    request.send(data);
                }

                function getKeyByValue(object, property, value) {
                  return Object.keys(object).find(key => object[key][property] === value);
                }
            }
        }
    }
</script>

<style scoped>
 input, button {
     margin: 10px 15px 15px 0;
 }

    p {
        font-weight: bold;
    }

</style>