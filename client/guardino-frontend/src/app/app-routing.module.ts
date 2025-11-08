import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LayoutShellComponent} from "./components/layout-shell/layout-shell.component";


const routes: Routes = [
  {path: '', redirectTo: '/login', pathMatch: 'full'},
  {path: '**', redirectTo: '', pathMatch: 'full', component: LayoutShellComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {

  constructor() {
  }

}
