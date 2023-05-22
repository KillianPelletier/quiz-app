import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/about",
      name: "AboutView",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/start-new-quiz-page",
      name: "NewQuizPage",
      component: () => import("../views/NewQuizPage.vue"),
    },
    {
      path: "/questions",
      name: "QuestionManager",
      component: () => import("../views/QuestionsManager.vue"),
    },
    {
      path: "/score",
      name: "ScorePage",
      component: () => import("../views/ScorePage.vue"),
    },
    {
      path: "/login",
      name: "LoginPage",
      component: () => import("../views/Admin/LoginPage.vue"),
    },
    {
      path: "/admin",
      name: "AdminPage",
      component: () => import("../views/Admin/AdminPage.vue"),
    },
  ],
});

export default router;
