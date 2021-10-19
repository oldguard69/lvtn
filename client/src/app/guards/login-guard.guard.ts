import { Injectable } from '@angular/core';
import { CanLoad, Route, Router, UrlSegment, UrlTree } from '@angular/router';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { setMesssages } from '../authentication/state/auth.actions';
import { selectIsLoggedIn } from '../authentication/state/auth.selectors';

@Injectable({
  providedIn: 'root'
})
export class LoginGuardGuard implements CanLoad {
  isLoggedIn$ = this.store.select(selectIsLoggedIn);
  constructor(private store: Store, private router: Router) {}
  
  canLoad(
    route: Route,
    segments: UrlSegment[]): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      let canAccess = false;
      this.isLoggedIn$
        .subscribe((isLoggedIn: boolean) => {
          if (isLoggedIn) {
            canAccess = true;
          } else {
            this.store.dispatch(
              setMesssages({
                messages: [
                  {
                    type: 'failure',
                    content: 'You need login before access.',
                  },
                ],
              })
            );
            this.router.navigateByUrl('/login');
          }
        })
        .unsubscribe();
      return canAccess;
  }
}
