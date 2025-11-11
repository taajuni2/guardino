import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AgentStatsCardComponent } from './agent-stats-card.component';

describe('AgentStatsCardComponent', () => {
  let component: AgentStatsCardComponent;
  let fixture: ComponentFixture<AgentStatsCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AgentStatsCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AgentStatsCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
