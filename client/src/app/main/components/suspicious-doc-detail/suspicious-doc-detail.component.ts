import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { GetSuspiciousDocDetail } from '../../state/actions';
import { selectSuspiciousDocDetail } from '../../state/selectors';

@Component({
  selector: 'app-suspicious-doc-detail',
  templateUrl: './suspicious-doc-detail.component.html',
  styleUrls: ['./suspicious-doc-detail.component.scss'],
})
export class SuspiciousDocDetailComponent implements OnInit {
  suspiciousDocDetail$ = this.store.select(selectSuspiciousDocDetail);
  private destroyed$ = new Subject<void>();
  constructor(private route: ActivatedRoute, private store: Store) {}

  ngOnInit(): void {
    console.log('here');

    this.route.params
      .pipe(takeUntil(this.destroyed$))
      .subscribe((param: any) =>
        this.store.dispatch(GetSuspiciousDocDetail({ id: param['id'] }))
      );
  }

  ngOnDestroy() {
    this.destroyed$.next();
    this.destroyed$.complete();
  }

  plagiarisedPercentage(num_of_sentences: number, num_of_plg_sentences: number): string {
    let percentage = num_of_plg_sentences * 100 / num_of_sentences;
    percentage = Number(percentage.toFixed(3));
    return `${percentage} %`;
  }
}
