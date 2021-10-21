import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { CalculateCosineSimResult, CosineSimService } from '../../services/cosine-sim.service';

@Component({
  selector: 'app-cosine-sim',
  templateUrl: './cosine-sim.component.html',
  styleUrls: ['./cosine-sim.component.scss']
})
export class CosineSimComponent implements OnInit {
  form = this.fb.group({
    'sent1': ['', Validators.required],
    'sent2': ['', Validators.required],
    'perform_cleaning': ['true', Validators.required]
  });
  result$ = new Observable<CalculateCosineSimResult>();


  constructor(
    private apiService: CosineSimService,
    private fb: FormBuilder
  ) { }

  ngOnInit(): void {
  }

  submit() {
    // return console.log(this.form.value);
    if (this.form.valid) {
      this.result$ = this.apiService.calculateCosineSimilarity(this.form.value);
    }
  }

  format(value: boolean): string {
    return value ? 'có': 'không';
  }

  get sent1() {
    return this.form.get('sent1')  as AbstractControl;
  }

  get sent2() {
    return this.form.get('sent2')  as AbstractControl;
  }

}
