import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SuspiciousDocDetailComponent } from './suspicious-doc-detail.component';

describe('SuspiciousDocDetailComponent', () => {
  let component: SuspiciousDocDetailComponent;
  let fixture: ComponentFixture<SuspiciousDocDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SuspiciousDocDetailComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SuspiciousDocDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
