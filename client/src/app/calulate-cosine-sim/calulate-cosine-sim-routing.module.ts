import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CosineSimComponent } from './components/cosine-sim/cosine-sim.component';

const routes: Routes = [
  { path: 'calculate-cosine-similarity', component: CosineSimComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class CalulateCosineSimRoutingModule {}
