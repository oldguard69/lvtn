import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import {MatRadioModule} from '@angular/material/radio';

import { CalulateCosineSimRoutingModule } from './calulate-cosine-sim-routing.module';
import { CosineSimComponent } from './components/cosine-sim/cosine-sim.component';
import { SharedModule } from '../shared/shared.module';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    CosineSimComponent
  ],
  imports: [
    CommonModule,
    CalulateCosineSimRoutingModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
    SharedModule,
    MatRadioModule,
    ReactiveFormsModule,
  ]
})
export class CalulateCosineSimModule { }
