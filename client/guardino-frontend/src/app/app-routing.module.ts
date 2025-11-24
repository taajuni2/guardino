import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LayoutShellComponent} from "./components/layout-shell/layout-shell.component";
import {AuthPageComponent} from "./components/auth-page/auth-page.component";
import {DashboardPageComponent} from "./components/dashboard-page/dashboard-page.component";
import {AgentsPageComponent} from "./components/agents-page/agents-page.component";
import {AuthGuard} from "./auth.guard";
import {EventsPageComponent} from "./components/events-page/events-page.component";


const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },

  // login ohne layout
  { path: 'login', component: AuthPageComponent },

  // alles hier braucht Auth
  {
    path: '',
    component: LayoutShellComponent,
       canActivate: [AuthGuard],          // schützt das Layout selbst
    children: [
         { path: 'dashboard', component: DashboardPageComponent },
         { path: 'agents', component: AgentsPageComponent },
         { path: 'events', component: EventsPageComponent },
      {path:'', redirectTo: 'dashboard', pathMatch: 'full' },
    ],
  },

  // fallback
  { path: '**', redirectTo: 'login' }
];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {

  constructor() {
  }

}
