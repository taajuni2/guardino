import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThreadTrendsComponent } from './thread-trends.component';

describe('ThreadTrendsComponent', () => {
  let component: ThreadTrendsComponent;
  let fixture: ComponentFixture<ThreadTrendsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ThreadTrendsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ThreadTrendsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
