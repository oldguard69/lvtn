import { TestBed } from '@angular/core/testing';

import { CosineSimService } from './cosine-sim.service';

describe('CosineSimService', () => {
  let service: CosineSimService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CosineSimService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
