import {Component} from '@angular/core';
import {Color, ScaleType} from "@swimlane/ngx-charts";

@Component({
  selector: 'app-thread-trends',
  templateUrl: './thread-trends.component.html',
  styleUrl: './thread-trends.component.scss'
})
export class ThreadTrendsComponent {
  data = [
    {name: 'Mon', value: 5},
    {name: 'Tue', value: 7},
    {name: 'Wed', value: 3},
    {name: 'Thu', value: 12},
    {name: 'Fri', value: 8},
    {name: 'Sat', value: 4},
    {name: 'Sun', value: 6}
  ];

  view: [number, number] = [400, 220];

  colorScheme: Color = {
    name: 'threats',
    selectable: true,
    group: ScaleType.Ordinal,
    domain: ['#ef4444'] // einheitlich rot
  };

  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = false;
  showXAxisLabel = "Days";
  showYAxisLabel = "Detection";
  animations = true;

}

