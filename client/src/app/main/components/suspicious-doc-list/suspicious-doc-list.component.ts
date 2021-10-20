import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { GetSuspiciousDocs } from '../../state/actions';
import { selectSuspiciousDocs } from '../../state/selectors';

@Component({
  selector: 'app-suspicious-doc-list',
  templateUrl: './suspicious-doc-list.component.html',
  styleUrls: ['./suspicious-doc-list.component.scss'],
})
export class SuspiciousDocListComponent implements OnInit {
  displayedColumns: string[] = ['filename', 'num-of-sentences', 'is-plg', 'view-detail'];
  suspiciousDocs$ = this.store.select(selectSuspiciousDocs);
  constructor(private store: Store) {}

  ngOnInit(): void {
    this.store.dispatch(GetSuspiciousDocs());
  }

  isFindPlagiarismParagraph(is_plg: Boolean): string {
    return is_plg ? 'Có' : 'Không'
  }
}
