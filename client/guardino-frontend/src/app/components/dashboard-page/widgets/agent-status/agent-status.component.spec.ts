import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AgentStatusComponent } from './agent-status.component';

describe('AgentStatusComponent', () => {
  let component: AgentStatusComponent;
  let fixture: ComponentFixture<AgentStatusComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AgentStatusComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AgentStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
