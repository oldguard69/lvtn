import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CosineSimComponent } from './cosine-sim.component';

describe('CosineSimComponent', () => {
  let component: CosineSimComponent;
  let fixture: ComponentFixture<CosineSimComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CosineSimComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CosineSimComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
