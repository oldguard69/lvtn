import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { combineLatest, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ResultComponent implements OnInit {
  src_name = 'src_6.txt';
  susp_name = 'susp_2.txt';

  vm$ = combineLatest([
    this.apiService.fetchSourceFileSentences(this.src_name),
    this.apiService.fetchSuspiciousFileSentences(this.susp_name),
    this.apiService.fetchStatOfSuspiciousFile(this.susp_name),
  ]).pipe(
    map(([src_sent, susp_sent, fileStat]) => ({
      src_sent,
      susp_sent,
      fileStat,
    }))
  );

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {}
}
