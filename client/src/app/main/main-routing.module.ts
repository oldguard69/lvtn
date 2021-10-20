import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DeactivateGuard } from '../guards/deactivate.guard';
import { IndexComponent } from './components/index/index.component';
import { ResultComponent } from './components/result/result.component';
import { SuspiciousDocDetailComponent } from './components/suspicious-doc-detail/suspicious-doc-detail.component';
import { SuspiciousDocListComponent } from './components/suspicious-doc-list/suspicious-doc-list.component';
import { UploadFileComponent } from './components/upload-file/upload-file.component';

const routes: Routes = [
  {
    path: '',
    component: IndexComponent,
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'upload-file' },
      {
        path: 'upload-file',
        component: UploadFileComponent,
        canDeactivate: [DeactivateGuard],
      },
      { path: 'result/:unique_filename', component: ResultComponent },
      { path: 'suspicious-docs', component: SuspiciousDocListComponent },
      { path: 'suspicious-docs/:id', component: SuspiciousDocDetailComponent },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class MainRoutingModule {}
