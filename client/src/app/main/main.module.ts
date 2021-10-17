import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';

import { MainRoutingModule } from './main-routing.module';
import { TextBoxComponent } from './components/text-box/text-box.component';
import { ResultComponent } from './components/result/result.component';
import { RawScrollComponent } from './components/raw-scroll/raw-scroll.component';
import { UploadFileComponent } from './components/upload-file/upload-file.component';

@NgModule({
  declarations: [
    TextBoxComponent,
    ResultComponent,
    RawScrollComponent,
    UploadFileComponent,
  ],

  imports: [
    CommonModule,
    MainRoutingModule,
    ScrollingModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule
  ],
})
export class MainModule {}
