import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-stat-cards',
  templateUrl: './stat-cards.component.html',
  styleUrl: './stat-cards.component.scss'
})
export class StatCardsComponent {
  @Input() totalAgents: number = 0;
  @Input() activeAgents = 0;
  @Input() threatsDetected = 0;



  public getPrecentage(activeAgents: number, totalAgents: number) {
    return totalAgents / activeAgents * 100;
  }
}

