<template>
  <div class="wrapper-outer">
   
    <b-container class="grid_nav"> 
        <header id="header_landing" >
            <div class="wrapper">
                    <div class="col-md-6" style= "float:left; margin-left: 5%">
                        <h1>DIGI BAR</h1>
                    </div>
            </div>
        </header>
        <div class="container-fluid">         
            <div class="sign-on" style="margin:  3rem  auto;">
                 <div class="wrapper-signin">
                    <b-container>
                    <b-row>
                        <b-col  class="signon-col">
                            <b-row align="left">
                                 <b-container id="signIn3">
                                    <p>Ab in deine Lieblingsbar</p>
                                    <b-form-input v-model="barId" placeholder="Bar Name" @change="urlUpdater" @keyup.enter="barCheck"></b-form-input>
                                    <b-button class="ourButton" @click="barCheck">Los Geht´s!</b-button>
                                    <span></span>
                                    <p id="p_city">Welche Digibars gibt es in meiner Stadt?</p>
                                    <div id=mySelect>
                                      <select id="dropdown_lp" class="dorpdown_custom">
                                      <option disabled value="">Bitte wähle eine Stadt aus</option>
                                      <option v-for="location in locations" :key="location.id">{{ location.city }}
                                      </option>
                                    </select>
                                    </div>
                                    <b-button id="city_btn" href="/bars" class="ourButton">Zeig mal!</b-button>
                                </b-container>
                            </b-row>
                        </b-col>
                        <b-col id="MiddleSep">
                                <b-row>
                                    <div class="verticalLine" ></div>
                                </b-row>
                         </b-col>
                        <b-col class = "signon-col">
                            <b-container id="signIn" style="margin=3rem 0 0 0;">  
                                <b-row align="left">
                                    <p>Du bist Bar Besitzer und willst deine digitale Bar kreieren?</p>
                                    <b-button id="setUpBtn" href="/barSetup" class="ourButton">Bar Eröffnen!</b-button>
                                    <span></span>
                                    <img id="wirvsvirus_img" src="../assets/landingpage/12-scaled.png" height="84" width="468"/>
                                </b-row>
                            </b-container>
                        </b-col>

                    </b-row>
                    </b-container>
                </div>
            </div>

        </div>
    </b-container>

      <div>
          <b-modal id="modal-1" title="Ungültiger Bar Name">
              <p class="my-4">Hey leider konnten wir die von dir gesuchte Bar nicht finden</p>
          </b-modal>
      </div>
  </div>
</template>

<script>

    export default {
        name: "landingPage",

        data() {
            return {
                barId: '',
                barUrl: '',
                plz: '',
                barName: '',
                locations: [
                    {
                        id: 0,
                        city: 'Konstanz'
                    },
                ]
            };
        },
        methods: {
            urlUpdater(){
                this.barUrl = '/bars/' + this.barId;
            },
            barCheck() {

                if(this.barUrl=="/" | this.barUrl==""){
                    this.$root.$bvModal.show('modal-1');
                    return [];
                }
                var request = new XMLHttpRequest();
                request.open('GET', this.$appConfig.backend_uri + 'bars', false);
                request.send();
                if (request.status === 200) {
                    var res = JSON.parse(request.responseText);
                    this.$router.push(this.barUrl);
                    //window.console.log(item.result);
                    return res;
                }
                this.$root.$bvModal.show('modal-1');
                return [];
            }
        },
        created(){

        }
    }
</script>

<style scoped>
 input, button {
     margin: 10px 15px 15px 0;
 }

    h1{
        font-size: 128px;
        font-style: italic;
        font-family: Oswald;
        color: #FFFFFF;
        letter-spacing: 15px;
        margin-top: 150px;
        margin-bottom: 40px;
    }
    p {
        font-weight: bold;
        font-size: 20px;
    }

    .verticalLine {
      position: absolute;
      background-color: lightgrey;
      width: 2px;
      top: 0px;
      bottom: 0px;
      left: 50%;
    }
    .title {
        margin: 10rpm
    }

    #mySelect select { 
        width:100%; }
</style>