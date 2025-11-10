import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatCardsComponent } from './stat-cards.component';

describe('StatCardsComponent', () => {
  let component: StatCardsComponent;
  let fixture: ComponentFixture<StatCardsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StatCardsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StatCardsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
