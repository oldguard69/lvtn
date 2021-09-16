import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { BehaviorSubject, combineLatest, Subject } from 'rxjs';
import { map, takeUntil, tap } from 'rxjs/operators';
import * as actions from '../../state/actions';
import {
  selectSourceFileList,
  selectSourceSentences,
  selectSuspiciousSentences,
  selectSuspiciousStats,
} from '../../state/selectors';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ResultComponent implements OnInit {
  susp_name = 'susp_2.txt';

  private doc_index = 0;
  private doc_list: string[] = [];
  private current_doc = new BehaviorSubject<string>(
    this.doc_list[this.doc_index]
  );
  current_doc$ = this.current_doc.asObservable();

  vm$ = combineLatest([
    this.store.select(selectSuspiciousStats),
    this.store.select(selectSourceSentences),
    this.store.select(selectSuspiciousSentences),
  ]).pipe(
    map(([fileStat, src_sent, susp_sent]) => ({
      fileStat,
      src_sent,
      susp_sent,
    }))
  );

  constructor(private store: Store) {}
  private destroyed$ = new Subject<void>();

  ngOnInit(): void {
    this.store.dispatch(
      actions.GetStatOfSuspiciousFile({ filename: this.susp_name })
    );
    this.store
      .select(selectSourceFileList)
      .pipe(takeUntil(this.destroyed$))
      .subscribe((files) => {
        this.doc_list = files;
        this.current_doc.next(files[0]);
      });
  }

  ngOnDestroy(): void {
    this.destroyed$.next();
  }

  load_prev_doc() {
    this.doc_index - 1 < 0 ? this.doc_index = this.doc_list.length - 1 : this.doc_index--;
    this.moveSourceFile();
  }

  load_next_doc() {
    this.doc_index = (this.doc_index + 1) % this.doc_list.length;
    this.moveSourceFile()
  }

  moveSourceFile() {
    this.store.dispatch(
      actions.GetSourceFileSentences({
        filename: this.doc_list[this.doc_index],
      })
    );
    this.current_doc.next(this.doc_list[this.doc_index]);
  }
}
