import landingPage from "@/components/landingPage"
import pubList from "@/components/pubList"
import pub from "@/components/pub"
import setup from "@/components/barSetUp"
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
      component: pub,
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