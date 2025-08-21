import { BrowserModule } from '@angular/platform-browser';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { AppComponent } from './app.component';
import {provideAnimationsAsync} from "@angular/platform-browser/animations/async";
import {AppRoutingModule} from "./app-routing.module";

/* the AppModule class with the @NgModule decorator */
@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
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
