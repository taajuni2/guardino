import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AgentsPageComponent } from './agents-page.component';

describe('AgentsPageComponent', () => {
  let component: AgentsPageComponent;
  let fixture: ComponentFixture<AgentsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AgentsPageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AgentsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
