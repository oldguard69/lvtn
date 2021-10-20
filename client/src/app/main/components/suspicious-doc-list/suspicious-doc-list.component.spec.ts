import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SuspiciousDocListComponent } from './suspicious-doc-list.component';

describe('SuspiciousDocListComponent', () => {
  let component: SuspiciousDocListComponent;
  let fixture: ComponentFixture<SuspiciousDocListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SuspiciousDocListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SuspiciousDocListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
