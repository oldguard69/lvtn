import { Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  Validators,
} from '@angular/forms';
import { Store } from '@ngrx/store';

import * as actions from '../../state/auth.actions';
import { selectAuthMessages } from '../../state/auth.selectors';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup = this.fb.group({
    email: ['', [Validators.email, Validators.required]],
    fullname: ['', Validators.required],
    password: ['', Validators.required],
  });
  constructor(private fb: FormBuilder, private store: Store) {}
  messages$ = this.store.select(selectAuthMessages);

  ngOnInit(): void {}

  handleSubmit() {
    console.log(this.registerForm.value);
    if (this.registerForm.valid) {
      this.store.dispatch(actions.register({ body: this.registerForm.value }));
    }
  }

  get fullname() {
    return this.registerForm.get('fullname') as AbstractControl;
  }

  get email() {
    return this.registerForm.get('email') as AbstractControl;
  }

  get password() {
    return this.registerForm.get('password') as AbstractControl;
  }
}
