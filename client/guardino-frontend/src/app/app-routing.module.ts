import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LayoutShellComponent} from "./components/layout-shell/layout-shell.component";
import {AuthPageComponent} from "./components/auth-page/auth-page.component";
import {DashboardPageComponent} from "./components/dashboard-page/dashboard-page.component";
import {AuthGuard} from "./auth.guard";


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
      // { path: 'agents', component: AgentsPageComponent },
      // { path: 'events', component: EventsPageComponent },
      // { path: 'settings', component: SettingsPageComponent },
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
