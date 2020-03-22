<template>
   <div id="wrapper">
     <b-container class="grid">
        <b-container id="container1"> 
              <div class="navi" style="font-size: 42px;">   
                <a id="arrow_link" href="/"> <img id="backArrowNav" class="backArrow" src="../assets/barsetup/back@2x.png" height="auto" width="35"/></a>
              </div>
              <div class="pubListCaption">
                  <div class ="justify-content-between">
                    <h2>
                      <div style= "float:left">Bars in deiner Stadt</div>
                      <div style ="float:right"><font color="green">{{city}}</font></div>
                    </h2>
                  </div>
              </div>
              <div class="container-fluid">
                <div class="publist">
                  <div class="publist-panel" v-for="item in items" :key="item.id">
                      <div class= "thumbnail">
                        <router-link v-bind:to="`/bars/${item.id}`">
                            <img :src= "item.image">
                        </router-link>
                      </div>

                      <div class= "caption" style = "float:left">
                        <h4>{{item.name}} </h4>
                        <p>{{item.description}} </p>
                      </div>
                      <div class = "user" style = "float:right">
                        {{item.users}} <span style = "font-size: 24px;"> <font-awesome-icon icon="user" /> </span>
                      </div>
                    </div>
                </div>

              </div>
      </b-container>
    </b-container>
  </div>
</template>

<script>

export default {
  name: 'pubList',

    data() {
      return {
          city: 'Konstanz'
      };
    },
    computed: {
      items: function() {
        var request = new XMLHttpRequest();
        request.open('GET', this.$appConfig.backend_uri + 'bars', false);
        request.send();
        window.console.log("test");
        if (request.status === 200) {
            var res = JSON.parse(request.responseText);

            //window.console.log(item.result);
            return res;
        }
        return []
      }
    },
  methods: {
    select: function(item) {
        alert(item.name);
    }
  },
}
</script>

<style>
  .publist {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
    grid-gap: 1rem;
    max-width: 80rem;
    margin: 5rem auto;

  }

  .publist-panel img {
    width: 95%;
    height: 20vw;
    object-fit: cover;
    border-radius: 0rem;
    margin-left: 10px;
    margin-right: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .pubListCaption {
    margin: 1rem auto;
  }
  .publist-panel {
    border:1px solid #D3D3D3;
    border-radius: 0rem;
  }
 .caption {
    margin-left: 10px;
    margin-right: 10px;
  }

  .navi {
    margin-top: 15px;
  }

  .user {
    margin-top: 30px;
    margin-right: 10px;
  }
  h1{
        font-family: Oswald;
        color: #000000;
        letter-spacing: 10.5px;
        margin-top: 100px;
        margin-bottom: 40px;
    }
</style>
