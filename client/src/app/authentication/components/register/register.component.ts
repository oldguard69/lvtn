import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup = this.fb.group({
    'email': ['', Validators.required],
    'name': ['', Validators.required],
    'password': ['', Validators.required],
  })
  constructor(private fb: FormBuilder) { }

  ngOnInit(): void {
  }

  handleSubmit() {
    console.log(this.registerForm.value)
  }

}
