import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-agent-status',
  templateUrl: './agent-status.component.html',
  styleUrl: './agent-status.component.scss'
})
export class AgentStatusComponent {
  @Input() online = 0;
  @Input() offline = 0;
  @Input() degraded = 0;   // optional, falls du später mehr States willst

  // ngx-charts expects [{name: string, value: number}, ...]
  chartData: { name: string; value: number }[] = [];

  view: [number, number] = [300, 220];

  // chart options
  showLegend = false;
  showLabels = false;
  isDoughnut = true;
  gradient = false;

  // Farben in der Reihenfolge deiner Daten
  colorScheme: any = { domain: ['#22c55e', '#ef4444', '#f97316'] };


  ngOnChanges(): void {
    this.chartData = this.buildChartData();
  }

  private buildChartData() {
    const data = [];
    if (this.online > 0) {
      data.push({ name: 'Online', value: this.online });
    }
    if (this.offline > 0) {
      data.push({ name: 'Offline', value: this.offline });
    }
    if (this.degraded > 0) {
      data.push({ name: 'Degraded', value: this.degraded });
    }
    return data;
  }
}
