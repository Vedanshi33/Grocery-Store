import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue';
import User_register from '../components/User_register.vue';
import User_login from '../components/User_login.vue';
import Admin_login from '../components/Admin_login.vue';
import AboutView from '../views/AboutView.vue';
import Edit_category from '../components/Edit_category.vue';
import Create_category from '../components/Create_category.vue';
import Add_product from '../components/Add_product.vue';
import View_categories from '../components/View_categories.vue';
import Categories_product from '../components/Categories_product.vue';
import Edit_product from '../components/Edit_product.vue';
import User_dashboard from '../components/User_dashboard.vue';
import Admin_dashboard from '../components/Admin_dashboard.vue';
import Cart_prod from '../components/Cart_prod.vue';
import Billing_page from '../components/Billing_page.vue';
import Thank_you from '../components/Thank_you.vue';
import Request_sm from '../components/Request_sm.vue';
import Admin_summary from '../components/Admin_summary.vue';
import Order_summary from '../components/Order_summary.vue';
import Sm_dash from '../components/Sm_dash.vue';



Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/about',
    
    component: AboutView

  },
  {
    path: '/User_register',
   
    component: User_register, 
  },
  {
    path: '/User_login',
    name: 'User_login',
    component: User_login, 
  },

  {
    path:'/Admin_login',

    component:Admin_login

  },


{
  
    
    path:'/Create_category',

    component:Create_category

  

},


{
  
    
  path:'/Request',

  component:Request_sm



},
{
  
    
  path:'/admin_summary',

  component:Admin_summary



},
{
  
    
  path:'/View_categories',

  component:View_categories



},
{
  
    
  path:'/User_dashboard',

  component:User_dashboard



},
{
  
    
  path:'/order_summary',

  component:Order_summary



},
{
  
    
  path:'/Admin_dashboard',

  component:Admin_dashboard



},

{
  
    
  path:'/sm_dashboard',

  component:Sm_dash



},

{
  path: '/Add_product/:category_id',
  

  component:Add_product,
  props: true

},
{
  path: '/category/:category_id',
  component: Categories_product,
  props: true

},
{
  path: '/cart',
  component: Cart_prod,
  props: true

},
{
  path: '/edit_category/:category_id',

  component:Edit_category,
  props: true

},
{
  path: '/edit_product/:category_id/:product_id',

  component:Edit_product,
  props: true

},
{
  
    
  path:'/billing',

  component:Billing_page



},
{
  path: '/confirmation',
  

  component:Thank_you,
 

},


];


const router = new VueRouter({
  routes,
});


export default router


