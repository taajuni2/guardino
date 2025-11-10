import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-stat-cards',
  templateUrl: './stat-cards.component.html',
  styleUrl: './stat-cards.component.scss'
})
export class StatCardsComponent {
  @Input() totalAgents = 0;
  @Input() activeAgents = 0;
  @Input() threatsDetected = 0;
}
