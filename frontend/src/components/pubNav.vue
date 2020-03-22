<template>
    <div id="wrapper_nav">
        <b-container class="grid_nav">
            <b-row>
                <b-col id="renderFrame" cols="8"><pub></pub></b-col>
                <b-col  id="nav_col">
                    <b-container id="container_nav">
                        <b-row >
                            <a id="arrow_link" href="/"> <img id="backArrowNav" class="backArrow" src="../assets/barsetup/back@2x.png" height="auto" width="35"/></a>
                        </b-row>
                        <b-row class="row_divider"  cols="8">
                            <h1 id="pubName_nav">{{bar.name}}</h1>
                        </b-row>
                        <b-row class="row_divider">
                            <h2>Unterstüze deine Bar</h2>
                            <b-container id="card_container">
                                <b-row id="card_row">
                                    <offer-cards v-bind:key=item.id v-for="item in items" :item="item"></offer-cards>
                                </b-row>
                                <b-button id="buy_btn" class="btn ourButton" type="submit" v-b-modal="'modal-1'">Kaufen</b-button>
                            </b-container>
                        </b-row>
                        <b-row class="row_divider">
                            <h2 id="offerTitle">Was gibt es für Angebote?</h2>
                            <b-container id="offerCont">
                                <b-row>
                                    <b-col class="offerLbl" cols="2">Bier</b-col>
                                    <b-col class="offerDesc">1€ Voucher - Kann nach Wiedereröffnung eingelöst werden</b-col>
                                </b-row>
                                <b-row>
                                    <b-col class="offerLbl" cols="2">Shot</b-col>
                                    <b-col class="offerDesc">Teilnahme am Gewinnspiel - Preis: Pub Quarantäne Survival Kit</b-col>
                                </b-row>
                                <b-row>
                                    <b-col class="offerLbl" cols="2">Quiz</b-col>
                                    <b-col class="offerDesc">Anmeldung zum Online Pub Quiz - Dienstag 20 Uhr</b-col>
                                </b-row>
                            </b-container>
                        </b-row>
                        <b-row class="row_divider">
                            <b-container>
                                <b-row id="greeting_row">
                                    <b-col id="greeting_pic" cols="3">
                                        <img src="../assets/barinterface/happy-1836445_640@2x.png" height="90"
                                             width="90"/>
                                    </b-col>
                                    <b-col id="greeting">
                                        <div id="greeting_wrapper">
                                            <p>Beste Grüße Euer</p>
                                            <h2>Heiko</h2>
                                        </div>
                                    </b-col>
                                    <b-col cols="2">

                                    </b-col>
                                </b-row>
                            </b-container>
                        </b-row>
                    </b-container>

                </b-col>

            </b-row>

        </b-container>

        <div>
        <b-modal id="modal-1" title="Kauf bestätigen">
            <img src="../assets/barinterface/paymentSelection.jpg" height="40%" width="40%"/>
        </b-modal>
    </div>
    </div>
</template>

<script>
    import OfferCards from "@/components/offerCards";
    import Pub from "@/components/pub"
    export default {
        name: "pubNav",
        components: {OfferCards, Pub},
        data() {
            return {
                items: [
                    {
                        id: 1,
                        lbl: 'Bier',
                        url: 'beer-311090_1280.png',
                        price: '1,00€',
                        imgWidth: '60%',
                    },
                    {
                        id: 2,
                        lbl: 'Shot!',
                        url: 'graphic-3578420_1280.png',
                        price: '1,00€',
                        imgWidth: '40%',
                    },
                    {
                        id: 3,
                        lbl: 'Pub Quiz',
                        url: 'question-4871181_1280.png',
                        price: '2,00€',
                        imgWidth: '46%',
                    }
                ]


            };
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
        }
    }

</script>

<style scoped>
    h2{
        font-family: Cardo;
        font-weight: bold;
        font-size: 25px;
    }

</style>