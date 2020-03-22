<template>
    <div class="container-fluid">

        <header>
            <div class="wrapper">
                <div class="img-container">
                    <img id="img_beer_lp" src="../assets/landingpage/cheers-839865_1920.png"/>
                    <h1 id="title_lp">DIGI BAR</h1>
                </div>
                <div>

                </div>
            </div>
        </header>
            <div class="sign-on">
            <div id="container2" class="grid-container">

                <div class="grid_clm ">
                        <p>Ab in deine Lieblingsbar</p>
                        <b-form-input v-model="barId" placeholder="Bar Id"></b-form-input>
                        <b-button href="/bars/0">Los Geht´s!</b-button>
                        <span></span>
                        <p id="p_city">Welche Digibars gibt es in meiner Stadt?</p>
                        <b-form-input v-model="plz" placeholder="Postleitzahl"></b-form-input>
                        <b-button href="/bars">Los Geht´s!</b-button>
                </div>

                <div class="grid_clm">

                </div>

                <div class="grid_clm">
                    <div class="wrapper_80">
                        <p>Du bist Bar Besitzer und willst deine digitale Bar kreieren?</p>
                        <b-button href="/barSetup" >Los Geht´s!</b-button>
                        <span></span>
                        <img id="wirvsvirus_img" src="../assets/landingpage/12-scaled.png" height="84" width="468"/>
                    </div>
                </div>
            </div>
        </div>

    </div>

</template>

<script>

    export default {
        name: "landingPage",

        data() {
            return {
                barId: '',
                plz: '',
                barName: '',
            };
        },
        methods: {

        },
        created(){

        }
    }
</script>

<style scoped>
 input, button {
     margin: 10px 15px 15px 0;
 }

    p {
        font-weight: bold;
        font-size: 20px;
    }

</style>