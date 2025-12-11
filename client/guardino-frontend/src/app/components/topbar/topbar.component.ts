import {Component, EventEmitter, Output, OnInit, OnChanges, SimpleChanges} from '@angular/core';
import {AuthService} from "../../services/auth-service/auth.service";

@Component({
  selector: 'app-topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss']
})
export class TopbarComponent implements  OnInit, OnChanges {
  @Output() toggleSidebar = new EventEmitter<void>();
  backendOnline: boolean = false;
  constructor(private authService: AuthService) {

  }

  ngOnInit() {
    this.authService.isOnline().subscribe((isUp) => {
      this.backendOnline = isUp;
    })
  }

ngOnChanges(changes: SimpleChanges) {

}


}
