import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanDeactivate, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { UploadFileComponent } from '../main/components/upload-file/upload-file.component';


@Injectable({
  providedIn: 'root'
})
export class DeactivateGuard implements CanDeactivate<UploadFileComponent> {
  canDeactivate(
    component: UploadFileComponent,
    currentRoute: ActivatedRouteSnapshot,
    currentState: RouterStateSnapshot,
    nextState?: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    return component.confirmExit();
  }
  
}
