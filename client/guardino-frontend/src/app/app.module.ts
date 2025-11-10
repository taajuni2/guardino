import { BrowserModule } from '@angular/platform-browser';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { AppComponent } from './app.component';
import {provideAnimationsAsync} from "@angular/platform-browser/animations/async";
import {AppRoutingModule} from "./app-routing.module";
import {LayoutShellComponent} from "./components/layout-shell/layout-shell.component";
import {SidebarComponent} from "./components/sidebar/sidebar.component";
import {TopbarComponent} from "./components/topbar/topbar.component";
import {AuthPageComponent} from "./components/auth-page/auth-page.component";
import {DashboardPageComponent} from "./components/dashboard-page/dashboard-page.component";
import {MatSidenavModule} from "@angular/material/sidenav";
import {MatCheckboxModule} from "@angular/material/checkbox";
import {FormsModule} from "@angular/forms";
import {MatButtonModule} from "@angular/material/button";
import {MatIconModule} from "@angular/material/icon";
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule }    from '@angular/material/list';
import { MatTooltipModule } from '@angular/material/tooltip';
import {MatFormField, MatLabel} from "@angular/material/form-field";
import {MatCard} from "@angular/material/card";
import {MatInput} from "@angular/material/input";

/* the AppModule class with the @NgModule decorator */
@NgModule({
  declarations: [
    AppComponent,
    LayoutShellComponent,
    SidebarComponent,
    TopbarComponent,
    AuthPageComponent,
    DashboardPageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatCheckboxModule,
    MatSidenavModule,
    FormsModule,
    MatButtonModule,
    MatIconModule,
    MatToolbarModule,
    MatListModule,
    MatTooltipModule,
    MatFormField,
    MatCard,
    MatLabel,
    MatInput,

  ],
  providers: [
  //  {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true},
   // {provide: DatePipe, useClass: DatePipe, multi: true},
    provideAnimationsAsync()
  ],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule { }
