import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RawScrollComponent } from './raw-scroll.component';

describe('RawScrollComponent', () => {
  let component: RawScrollComponent;
  let fixture: ComponentFixture<RawScrollComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RawScrollComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RawScrollComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
