import { Component } from '@angular/core';
import { Store } from '@ngrx/store';
import { loadAuthTokenFromLocalStorage } from './authentication/state/auth.actions';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'client';

  ngOnInit() {
    this.store.dispatch(loadAuthTokenFromLocalStorage());
  }

  constructor(private store: Store) {}
}
