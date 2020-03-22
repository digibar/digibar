<template>
    <b-col class="card_col">

            <div v-bind:class=this.class v-on:click="toggleIsClicked">
                <img class="item_pic" v-bind:src=imageSrc :style="{'width': item.imgWidth}"/>
                <p class="item_lbl" :style="{'display': lblHidden}">{{item.lbl}}</p>
                <p class="item_price" :style="{'display': priceHidden}">{{item.price}}</p>
            </div>

    </b-col>
</template>

<script>
    export default {
        name: "offerCards",
        props: ['item'],
        data() {
            return {
                isClicked: false,
                class: 'card',
                lblHidden: 'none',
                priceHidden: 'none'
            };
        },
        methods: {
            toggleIsClicked: function(){
                if(this.class=="card"){
                    this.class = "card_clicked";
                    this.lblHidden = '';
                    this.priceHidden = '';
                } else{
                    this.class = "card";
                    this.lblHidden = 'none';
                    this.priceHidden = 'none';
                }

            }
        },
        computed: {
            imageSrc: function () {
                return require('../assets/barinterface/' + this.item.url);
            }
        }
    }
</script>

<style scoped>

    .item_lbl {
        margin-bottom: 0;
    }

    .item_pic {
        align-self: center;
        margin-top: 10px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .item_price {
        position: relative;
        top: -5px;
        font-weight: bold;
        margin-bottom: 0;
        height: 100%;
        width: 100%;
    }

    .card {
        width: 100px;
        padding: 5px;
        margin: 20px 5px 5px 0px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    .card,.card_clicked {
        cursor: pointer;
    }

    .card p{
        font-family: Cardo;
    }

    .card_clicked p {
        text-align: left;
        font-family: Cardo;
    }

    .card_clicked {
        width: 100px;
        padding: 5px;
        margin: 20px 5px 5px 0px;
        background-color: #90CA47;
        text-align: center;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        border-style: solid;
        border-color: #359425;
    }

    a{
        text-decoration: none;
    }
</style>