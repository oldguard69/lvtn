import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup = this.fb.group({
    'email': ['', Validators.required],
    'password': ['', Validators.required]
  })
  constructor(private fb: FormBuilder) { }

  ngOnInit(): void {
  }

  handleSubmit() {
    console.log(this.loginForm.value);
  }

}
