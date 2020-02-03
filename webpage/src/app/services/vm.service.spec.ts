import { TestBed } from '@angular/core/testing';

import { VmService } from './vm.service';

describe('VmService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: VmService = TestBed.get(VmService);
    expect(service).toBeTruthy();
  });
});
