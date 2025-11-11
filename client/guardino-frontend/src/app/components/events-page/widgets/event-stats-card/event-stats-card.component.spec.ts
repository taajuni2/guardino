import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventStatsCardComponent } from './event-stats-card.component';

describe('EventStatsCardComponent', () => {
  let component: EventStatsCardComponent;
  let fixture: ComponentFixture<EventStatsCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EventStatsCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EventStatsCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
