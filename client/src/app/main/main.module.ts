import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import {MatDividerModule} from '@angular/material/divider';
import { MainRoutingModule } from './main-routing.module';
import {MatProgressBarModule} from '@angular/material/progress-bar';

import { TextBoxComponent } from './components/text-box/text-box.component';
import { ResultComponent } from './components/result/result.component';
import { RawScrollComponent } from './components/raw-scroll/raw-scroll.component';
import { UploadFileComponent } from './components/upload-file/upload-file.component';
import { IndexComponent } from './components/index/index.component';
import { SharedModule } from '../shared/shared.module';
import { SuspiciousDocListComponent } from './components/suspicious-doc-list/suspicious-doc-list.component';
import { SuspiciousDocDetailComponent } from './components/suspicious-doc-detail/suspicious-doc-detail.component';

@NgModule({
  declarations: [
    TextBoxComponent,
    ResultComponent,
    RawScrollComponent,
    UploadFileComponent,
    IndexComponent,
    SuspiciousDocListComponent,
    SuspiciousDocDetailComponent,
  ],

  imports: [
    CommonModule,
    MainRoutingModule,
    ScrollingModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
    SharedModule,
    MatTableModule,
    MatDividerModule,
    MatProgressBarModule
  ],
})
export class MainModule {}
