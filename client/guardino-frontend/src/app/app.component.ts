import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {WebsocketService} from "./services/websocket-service/websocket.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements  OnInit {
  title = 'guardino-frontend';

  constructor(private websocketService: WebsocketService) {
  }
  ngOnInit() {
    this.websocketService.connect();
  }
}
