import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { IndexComponent } from './components/index/index.component';
import { ResultComponent } from './components/result/result.component';
import { UploadFileComponent } from './components/upload-file/upload-file.component';

const routes: Routes = [
  {
    path: '',
    component: IndexComponent,
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'upload-file'},
      { path: 'upload-file', component: UploadFileComponent },
      { path: 'result', component: ResultComponent },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class MainRoutingModule {}
