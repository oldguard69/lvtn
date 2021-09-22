import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ScrollingModule } from '@angular/cdk/scrolling';

import { MainRoutingModule } from './main-routing.module';
import { TextBoxComponent } from './components/text-box/text-box.component';
import { ResultComponent } from './components/result/result.component';
import { RawScrollComponent } from './components/raw-scroll/raw-scroll.component';

@NgModule({
  declarations: [TextBoxComponent, ResultComponent, RawScrollComponent],

  imports: [CommonModule, MainRoutingModule, ScrollingModule],
})
export class MainModule {}
