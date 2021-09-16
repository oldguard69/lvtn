import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { BehaviorSubject, combineLatest, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ResultComponent implements OnInit {
  susp_name = 'susp_2.txt';

  private doc_index = 0;
  private doc_list = ['src_6.txt', 'src_1.txt', 'src_0.txt', 'src_8.txt', 'src_5.txt']
  private current_doc = new BehaviorSubject<string>(this.doc_list[this.doc_index]);
  current_doc$ = this.current_doc.asObservable();
  src_sents = this.apiService.fetchSourceFileSentences(this.current_doc.value);
  constructor(private apiService: ApiService) {}

  vm$ = combineLatest([
    this.src_sents,
    this.apiService.fetchSuspiciousFileSentences(this.susp_name),
    this.apiService.fetchStatOfSuspiciousFile(this.susp_name),
  ]).pipe(
    map(([src_sent, susp_sent, fileStat]) => ({
      src_sent,
      susp_sent,
      fileStat,
    }))
  );

 

  ngOnInit(): void {}

  load_prev_doc() {
    this.doc_index = (this.doc_index - 1) % this.doc_list.length;
    this.current_doc.next(this.doc_list[this.doc_index]);
    this.src_sents = this.apiService.fetchSourceFileSentences(this.current_doc.value);
  }

  load_next_doc() {
    this.doc_index = (this.doc_index + 1) % this.doc_list.length;
    this.current_doc.next(this.doc_list[this.doc_index]);
    this.src_sents = this.apiService.fetchSourceFileSentences(this.current_doc.value)
  }
}
