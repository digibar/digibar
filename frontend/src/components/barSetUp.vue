<template>

    <div id="content_barS">

        <div id="gridContainer3">

            <div id="img_barS"></div>

            <div id="signUpForm">
                <a href="/"> <img class="backArrow" src="../assets/barsetup/back@2x.png" height="auto" width="35"/></a>
                <h1>Herzlich Wilkommen</h1>
                <b-alert :show="alert" dismissible variant="danger">{{err_msg}}</b-alert>
                <h2>Bar anlegen</h2>
                <p style="margin-bottom: 30px">Bitte fülle die Daten zu deiner Bar hier aus</p>

                <b-form @submit="onSubmit" @reset="onReset" v-if="show">

                    <b-form-group id="input-group-1" label="Bar Name:" label-for="input-12">
                        <b-form-input
                                id="input-1"
                                v-model="form.name"
                                required
                                placeholder="Bar Name"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group id="input-group-2" label="Beschreibung:" label-for="input-2">
                        <b-form-input
                                id="input-2"
                                v-model="form.description"
                                required
                                placeholder="PLZ"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group id="input-group-3" label="Bild von deiner Bar (URL-Format):" label-for="input-3">
                        <b-form-input
                                id="input-3"
                                v-model="form.image"
                                required
                                placeholder="Bild URL"
                        ></b-form-input>
                    </b-form-group>

                    <b-button v-on:click="onSubmit" href="/bars/0" id="barS_btn1" class="btn" type="submit">Anmelden</b-button>
                </b-form>

            </div>


        </div>

    </div>

</template>

<script>
    import {bus} from '../main';

    export default {
        data() {
            return {
                form: {
                    name: '',
                    description: '',
                    image: '',
                },
                show: true,
                alert: false,
                err_msg: '',
            }
        },
        created() {
          bus.$on('barNameChanged', (data) => {
              console.log(data);
              this.name = data;
            })
        },
        computed: {

        },
        methods: {

            onSubmit(evt) {
                console.log("onSubmit Methode getriggert");
                evt.preventDefault();

                if(!this.urlCheck(this.form.image)){
                    this.alert=true;
                    this.err_msg = 'Bitte eine gültige URL eingeben';
                    return [];
                }
                this.alert=false;

                var json = JSON.stringify(this.form);
                var request = new XMLHttpRequest();
                var id = encodeURIComponent(this.form.name.toLowerCase().replace(/[ ]/g, '-').replace(/[^a-z0-9-]/g, ''));
                request.open('PUT', this.$appConfig.backend_uri + 'manage/bars/' + id, false);
                request.send(json);

                if (request.status === 201) {
                    var res = JSON.parse(request.responseText);
                    window.console.log(res);
                    //window.console.log(item.result);
                    this.$router.push({'name': 'bars'})
                    return res;
                }
                this.err_msg = 'Keine Verbindung zum Server möglich';
                return []
            },

            onReset(evt) {
                evt.preventDefault()
                // Reset our form values
                this.form.email = ''
                this.form.name = ''
                this.form.food = null
                this.form.checked = []
                // Trick to reset/clear native browser form validation state
                this.show = false
                this.$nextTick(() => {
                    this.show = true
                })
            },

            urlCheck(str) {
                var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
                        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
                        '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
                        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
                        '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
                        '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
                return !!pattern.test(str);
            }

        }
    }
</script>

<style scoped>
    .responsive {
        width: 100%;
        height: auto;
    }

    h1{
        font-family: Oswald;
        color: #7A8286;
        letter-spacing: 10.5px;
        margin-top: 100px;
        margin-bottom: 40px;
    }


</style>