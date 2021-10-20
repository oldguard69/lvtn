import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { BehaviorSubject, combineLatest, Subject } from 'rxjs';
import { map, takeUntil, tap } from 'rxjs/operators';
import * as actions from '../../state/actions';
import {
  selectSourceFileList,
  selectSourceSentences,
  selectSuspiciousSentences,
  selectSuspiciousStats,
  selectSentenceIndex
} from '../../state/selectors';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ResultComponent implements OnInit {
  // susp_name = 'susp_5.txt_2ceeb2a7-1491-455d-9c8b-ae536dca241d';

  private doc_index = 0;
  private source_doc_list: string[] = [];
  private current_source_doc = new BehaviorSubject<string>(
    this.source_doc_list[this.doc_index]
  );
  current_source_doc$ = this.current_source_doc.asObservable();

  vm$ = combineLatest([
    this.store.select(selectSuspiciousStats),
    this.store.select(selectSourceSentences),
    this.store.select(selectSuspiciousSentences),
    this.store.select(selectSentenceIndex)
  ]).pipe(
    map(([fileStat, src_sent, susp_sent, sentIndex]) => ({
      fileStat,
      src_sent,
      susp_sent,
      sentIndex
    }))
  );

  constructor(private store: Store, private route: ActivatedRoute) {}
  private destroyed$ = new Subject<void>();

  ngOnInit(): void {
    this.route.params.pipe(
      takeUntil(this.destroyed$),
    ).subscribe(
      (param) =>
        this.store.dispatch(
          actions.GetStatOfSuspiciousFile({ filename: param['unique_filename'] })
        )
    );

    this.store
      .select(selectSourceFileList)
      .pipe(takeUntil(this.destroyed$))
      .subscribe((files) => {
        this.source_doc_list = files;
        this.current_source_doc.next(files[0]);
      });
  }

  ngOnDestroy(): void {
    this.destroyed$.next();
    this.destroyed$.complete();
  }

  load_prev_doc() {
    this.doc_index - 1 < 0
      ? (this.doc_index = this.source_doc_list.length - 1)
      : this.doc_index--;
    this.moveSourceFile();
  }

  load_next_doc() {
    this.doc_index = (this.doc_index + 1) % this.source_doc_list.length;
    this.moveSourceFile();
  }

  private moveSourceFile() {
    this.store.dispatch(
      actions.GetSourceFileSentences({
        filename: this.source_doc_list[this.doc_index],
      })
    );
    this.current_source_doc.next(this.source_doc_list[this.doc_index]);
    this.store.dispatch(actions.SetCurrentSentencesIndex({index: this.doc_index}));
  }
}
