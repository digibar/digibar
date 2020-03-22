import landingPage from "@/components/landingPage"
import pubList from "@/components/pubList"
import setup from "@/components/barSetUp"
import pubNav from "@/components/pubNav"
import pub3DView from "@/components/pub3DView"

export default [
    {
        path: '/',
        component: landingPage
    },
    {
        path: '/bars',
        name: 'bars',
        component: pubList
    },
    {
      path: '/bars/:id',
      name: 'pub',
      component: pubNav,
    },
    {
        path: '/barSetup',
        component: setup
    },
	{
        path: '/bar3D',
        component: pub3DView
    }
]