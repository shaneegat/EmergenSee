import { Injectable } from '@angular/core';
import { Account } from '../Modules/account/accountModule';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { ApiService } from './api.service';
import { AccountMapper } from '../Mappers/account.mapper';

export interface LoginResponse {
  success: boolean;
  account: Account;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private userState = new BehaviorSubject<any>(this.getUserFromLocalStorage());
  userState$ = this.userState.asObservable();

  constructor(private apiService: ApiService) {}

  setUser(user: any) {
    const publicUser = user ? { id: user.id, name: user.name, role: user.role } : null;
    this.userState.next(publicUser);
    this.setUserInLocalStorage(publicUser);
  }

  login(credentials: any): Observable<any> {
    return this.apiService.login(credentials).pipe(
      tap(response => {
        if (response.success) {
          const user = AccountMapper.mapToAccount(response.account);
          this.setUser(user);
        }
      })
    );
  }

  logout() {
    this.userState.next(null);
    this.clearLocalStorage();
  }

  getId(): number {
    const user = this.userState.getValue();
    return user ? user.id : null;
  }

  getName(): string {
    const user = this.userState.getValue();
    return user ? user.name : '';
  }

  getRole(): number {
    const user = this.userState.getValue();
    return user ? user.role : 0;
  }

  private setUserInLocalStorage(user: any) {
    localStorage.setItem('user', JSON.stringify(user));
  }

  private getUserFromLocalStorage(): any {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  private clearLocalStorage() {
    localStorage.removeItem('user');
  }
}